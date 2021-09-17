# URLs Sources
The URLs-grab project at https://github.com/ArchiveTeam/urls-grab allows for URLs to be archived, alongside the page requisite, and optionally other found pages. This repository contains the lists of URLs to be periodically queued and instructions on how to structure the items.

## How to queue
The repository contains txt files, which follow a pattern `[0-9]+_STRING.txt`, where `STRING` is some string to identify the contents of the txt file, and `[0-9]+` is the interval for how often the items in the txt file should be queued to the tracker. Multiple files with equal intervals and differents names can be created. Lines can be added and removed from the txt files.

Each txt file contains a list of parameters joined with `;`, where the URLs are not percent encoded for simplicity. See the section on 'Custom URL item' to find the allowed parameters. A special case is the `random` parameter. If this parameter is specified (in our example case `3600_EXAMPLE.txt` with value `RANDOM`), a random value will be assigned automatically every time the custom item is queued.

***warning***: The URLs-grab project can easily overload websites if too many URLs are queued at once.

## Custom URL item
Custom URL items contain the URL to be archived and a number of settings showing how to extract and queue subsequent URLs. These items are formatted as `custom:PARAMS` where `PARAMS` is an URL-encoded set of parameters. These parameters are:
 * `url`: The URL to be archived.
 * `random`: A random string. Items queued to URLs-grab are deduplicated through a bloom filter with items previously queued. This `random` parameter allows for URLs to be requeued.
 * `keep_random`: The depth up to which the `random` string shall be preserved. If `keep_random` is larger than 0, any discovered URLs to be queued will be queued with parameter `keep_random=keep_random-1`, and have the `random` parameter copied over.
 * `all`: Whether all extracted URLs should be queued, or only the page requisites.
 * `keep_all`: Similar to `keep_random`, but for `all`.
 * `depth`: The depth up to which to queue `custom` items. If depth is larger than 0, any URLs found will be queued as `custom` item, else as regular URL item.
 * `deep_extract`: If set to 1, patterns will be used to extract hardcoded URLs that are not extracted by Wget-Lua itself, for example from any scripts. This parameter is only kept on the initial queued URL, not any subsequently queued URLs. This should be used on for example RSS feeds.

### Examples
The following items are example items
 * `custom:url=https%3A%2F%2Fexample.com%2F&all=1&deep_extract=1` decodes to `{'url': 'https://example.com/', 'all': 1, 'deep_extract': 1}`.

   This will archive https://example.com/, and queue all URLs (not limited to page requisites) that can be extracted from the webpage using both Wget-Lua extraction and patterns to extract hardcoded URLs. If this item was already queued before, it will be ignored now. Parameter `depth` is not specified, effectively setting it to 0.

 * `custom:url=https%3A%2F%2Fexample.com%2F&all=1&deep_extract=1&random=sa7ff8pjss&depth=2&keep_random=1&keep_all=2` decodes to `{'url': 'https://example.com/', 'all': 1, 'deep_extract': 1, 'random': 'sa7ff8pjss', 'depth': 2, 'keep_random': 1, 'keep_all': 2}`.

   This includes the `random` string, thus making sure it is queued even if a similar item was queued before. `depth` is set to 2, so `custom` items will be queued for the found URLs which will all have parameter `all`, effectively allowing a recursive crawl up to depth 3. `keep_random` has value 1, so only the next queued `custom` items will have the `random` value copied over, and subsequently queued `custom` will not. `deep_extract` is only kept for the very first item. `keep_all` is set to 2, which is equal to `depth`, so the `all=1` parameter will be copied over for all depths.

   Any found URLs will be queued with parameters `{'url': URL, 'all': 1, 'random': 'sa7ff8pjss', 'depth': 1, 'keep_random': 0, 'keep_all': 1}`, note that parameter `deep_extract` is removed, `depth`, `keep_random`, and `keep_all` are reduced by 1, and `random` is copied over.
   
