import polars as pl
import json
from anthropic.types.text_block import TextBlock
from anthropic_client import AnthropicClient


def parse_json(
    message: TextBlock,
) -> tuple[pl.DataFrame, bool]:
    """Attempts to parse JSON from an anthropic TextBlock.

    Just tries to shove the provided message into JSON. If it fails, we return
    False, signaling for a retry.
    """
    try:
        valid_json = json.loads(message.text)
    except json.JSONDecodeError:
        return pl.DataFrame(), False
    df = pl.DataFrame(valid_json)
    return df, True


def find_clients(
    existing_clients: list[str], anthropic_client: AnthropicClient
) -> pl.DataFrame:
    """Finds clients for Ascent!

    The purpose of this function is a first, high level search of names of potential clients.
    We do not ask for much detail here, just who they are, some basic links, and why the AI
    thinks they might be a good choice.

    existing_clients: A list of strings containing the names of organizations already in our
        contact list. We will instruct the AI to avoid these.

    """

    prompt = f"""
        Begin by searching the web for companies in Cincinati, Dayton, and Northern Kentucky 
        that would be great clients for Ascent Data Insights.
        Provide me with your top 5 choices.

        Below is a list of existing clients we have contacted already, do not include anyone from this list
        in your recommendations.
        {existing_clients}

        Focus on companies that are small to medium sized businesses, such as HVAC, Home Services, Restaurants, etc. 
        Companies like tech startups should be ignored. Healthcare is okay, but should be deprioritized.

        Return your result as valid JSON List with an entry per company in the following format: 
        "Organization" (string), "Industry" (string), "Links" (list[string]), "Reason" (string)

        ONLY return the JSON and no other text. You can include your reason for choosing this company in the "Reason" section of the JSON.
        There should be no text before the JSON, and no text after the JSON. Every field must contain information, links are not
        allowed to be empty or null. Provide links for every company.
    """

    success = False
    attempts = 1
    df = None
    while not success and attempts <= 5:

        print(f"Client search attempt {attempts} ...")
        message = anthropic_client.create_message(prompt=prompt)

        final_message = message.content[-1]
        assert isinstance(
            final_message,
            TextBlock,
        )
        df, success = parse_json(message=final_message)
        attempts += 1

    if df is None:
        raise ValueError("Failed to generate valid JSON")

    print("New Leads Generated!")
    print(df)
    return df


def research_client(
    organization: pl.Series, anthropic_client: AnthropicClient
) -> pl.DataFrame:
    """Provides deeper, in depth research on a particular potential client.

    Args:
        organization: A series of info on the company we want to do business on. Should
            be a row from find_clients().

    Returns:
        Another polars series with added information about the lead.
    """

    prompt = f"""
        Please do some web search research on the business **{organization}** in the Greater Cincinnati
        area. We would like to answer the following questions:

        * Who should we contact to try to pitch this company? Typically this will be an owner or CTO.
        * What is their name, work email, and/or work phone number?
        * If they have a generic email or phone nuber for the business, get that as well.
        * Estimated Revenue 
        * Estimated Employee Count
        * Any mentions they have in news articles or journals
        * Any mentions of technologies they use, like databases, SaaS companies, cloud providers, etc.
        * Do broader research on this industry and help us understand the big trends in this industry right now.
        * Call out three important details about this company.

        Return your result as valid JSON List with an entry per company in the following format: 
        "Organization" (string), Contact Name (string), Contact Role (string), Contact Phone Number (string),
        Contact Email (string), Contact Citation [string], Generic Email (string), Generic Phone Number (string), Generic Citation [string],
        Revenue (number), Headcount (number), News Mention Citations (List[string])
        Technologies Used (List[string]), Technologies Used Citations [list[string]], Trends in Industry (List[string]),
        Trends in Industry Citations [list[string][, Important Details (List[string]), Important Details Citations [list[string]].

        ONLY return the JSON and no other text. There should be no text before the JSON, and no text after the JSON. 
        Each of the "Citations" Fields should contain a valid URL to where you got this particular information. Double check
        that all provided links are valid and go to live web pages referencing where you got that particular information.
    """

    success = False
    attempts = 1
    df = None
    while not success and attempts <= 5:

        print(f"Client research attempt {attempts} ...")
        message = anthropic_client.create_message(prompt=prompt)

        final_message = message.content[-1]
        assert isinstance(
            final_message,
            TextBlock,
        )
        df, success = parse_json(message=final_message)
        attempts += 1

    if df is None:
        raise ValueError("Failed to generate valid JSON")

    print("Research Generated!")
    print(df)
    return df
