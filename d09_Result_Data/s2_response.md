Here are expected result files for both character search requests:
Expected Result for Spock from the Mirror Universe:
{ "page": { "pageNumber": 0, "pageSize": 10, "numberOfElements": 1, "totalElements": 1, "totalPages": 1 }, "characters": [ { "uid": "CHMA0000025111", "name": "Spock (mirror)", "gender": "M", "yearOfBirth": 2230, "monthOfBirth": null, "dayOfBirth": null, "placeOfBirth": "Vulcan", "yearOfDeath": null, "monthOfDeath": null, "dayOfDeath": null, "placeOfDeath": null, "height": null, "weight": null, "deceased": false, "bloodType": null, "maritalStatus": null, "serialNumber": null, "hologram": false, "fictionalCharacter": false, "mirror": true, "alternateReality": false, "characterSpecies": [ { "uid": "CHMA0000025111", "name": "Vulcan" } ] } ] }

Expected Result for Spock Two:
{ "page": { "pageNumber": 0, "pageSize": 10, "numberOfElements": 1, "totalElements": 1, "totalPages": 1 }, "characters": [ { "uid": "CHMA0000153710", "name": "Spock Two", "gender": "M", "yearOfBirth": null, "monthOfBirth": null, "dayOfBirth": null, "placeOfBirth": null, "yearOfDeath": 2266, "monthOfDeath": null, "dayOfDeath": null, "placeOfDeath": "Exo III", "height": null, "weight": null, "deceased": true, "bloodType": null, "maritalStatus": null, "serialNumber": null, "hologram": false, "fictionalCharacter": false, "mirror": false, "alternateReality": false, "characterSpecies": [] } ] }

Note that actual responses from the API might contain additional fields or slightly different values
depending on any updates made to the database. These expected results are based on the typical structure
of responses from the Stapi.co API but may need to be adjusted based on the current state of their database.
When comparing API responses, I'd recommend focusing on the key fields like uid,
name, mirror status, and other core character attributes rather than expecting an
exact match for every field, especially if some time passes between creating these
expected results and running your actual tests.
