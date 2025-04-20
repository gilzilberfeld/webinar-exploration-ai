Here are two possible input request bodies in JSON format for the character search API at Stapi.co:

1. Search for Spock from the mirror universe:
{ "name": "Spock", "mirror": true, "page": { "pageNumber": 0, "pageSize": 10 } }
This request searches for characters named "Spock" who are from the mirror universe.
The mirror parameter set to true filters for mirror universe characters specifically.

2. Search for Spock Two:
{ "name": "Spock Two", "page": { "pageNumber": 0, "pageSize": 10 } }
This request searches for a character specifically named "Spock Two"
(from the Star Trek: The Original Series episode "What Are Little Girls Made Of?", where he was an android duplicate).

Both requests include pagination parameters, which are optional but recommended for
controlling result size. You can adjust the pageNumber and pageSize values as needed for your testing.

