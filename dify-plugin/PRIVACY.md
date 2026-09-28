# Privacy Policy, TableJourney Plugin

This plugin connects Dify to TableJourney's public agent API at
`https://tablejourney.com/api/v1`. The API is read-only and requires no
account or API key.

## What is collected and sent

When a tool from this plugin is invoked, the plugin sends only the
parameters that tool call carries, as HTTPS GET query parameters (or, for
`plan_day`, as part of the request path) to `tablejourney.com`. Depending
on the tool, that is a mix of:

* A free-text search query, city, country, cuisine, dietary need, price
  tier, coordinates, date, date range, or partner name that you or the
  calling LLM supplied as tool input.
* The optional API key, if you configured one in the provider credentials,
  sent as an `X-API-Key` header. This key exists only for TableJourney's
  own attribution reporting; it is never required.

This plugin does not send your Dify prompts, chat history, account
identifiers, IP address, or any data beyond the specific tool parameters
above. TableJourney's own web server still logs the IP address and
user-agent of the HTTPS request it receives, the same way it logs any
request to its site; see TableJourney's site privacy policy below.

## What the plugin itself stores

This plugin does not persist queries, results, or your API key anywhere
outside of the Dify runtime. Each tool call is a single stateless HTTPS
request; nothing is cached or logged by the plugin code.

Dify itself may store tool inputs, outputs, and logs according to your
own Dify deployment's configuration; that is governed by Dify's own
privacy policy, not by this plugin.

## Where it goes

The only third party this plugin talks to is TableJourney
(`tablejourney.com`), operated by Rowie LLC. TableJourney's site privacy
policy is at [tablejourney.com/privacy/](https://tablejourney.com/privacy/).
It covers standard web server logging (IP address, user agent, requested
URL, timestamp) and does not sell data or build cross-site profiles. It
does not separately mention the agent API, because the API receives the
same kind of request (an HTTPS GET with query parameters) as any page
load on the site and is covered by the same logging practice.

## Credential handling

* The optional `api_key` credential is declared as a Dify `secret-input`.
  Dify encrypts it at rest and never echoes it back to clients.
* This plugin's error messages never include the credential value.
* TableJourney's API works identically with or without this key; no
  private or personal data is unlocked by supplying one.

## Contact

For privacy questions about this plugin: support@tablejourney.com
