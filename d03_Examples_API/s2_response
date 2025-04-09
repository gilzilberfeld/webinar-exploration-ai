"Based on the Star Trek API documentation, here are examples for each of the test charters:

1. **Basic search functionality**:
   - Search for "Kirk" to verify James T. Kirk appears in results
   - Search for "Picard" to confirm Jean-Luc Picard data retrieval
   - Search for "Spock" to verify character data matches canonical information

2. **Pagination parameters**:
   - Set pageNumber=0 and pageSize=10 to verify first page returns 10 results
   - Test with pageSize=100 (maximum allowed) to verify proper handling
   - Request pageNumber beyond available results to test boundary behavior

3. **Search filters**:
   - Filter by gender=F to verify only female characters returned
   - Filter by status=DECEASED to check for accurate character status
   - Combine filters (e.g., species=HUMAN and gender=M) to test multiple parameter handling

4. **Error handling**:
   - Send malformed JSON body to verify appropriate 400 error response
   - Test with invalid parameters (e.g., pageSize=-1) to check error handling
   - Send request with incorrect content type to verify proper error messaging

5. **Special characters and Unicode**:
   - Search for characters with apostrophes (e.g., "T'Pol")
   - Search for characters with non-Latin names like "Worf, son of Mogh" with Klingon text
   - Test with escaped characters to verify parser handling

6. **Performance boundaries**:
   - Create complex query with multiple filters (gender, species, status, hologram)
   - Test with maximum allowed pageSize (100) to measure response time
   - Send rapid consecutive requests to test rate limiting behavior

7. **Concurrent requests**:
   - Send 10 simultaneous search requests with different parameters
   - Test with 5 identical requests sent simultaneously
   - Alternate between heavy and light queries in rapid succession

8. **Response format consistency**:
   - Compare response structure between empty results and multiple results
   - Verify character objects maintain same schema across different searches
   - Check consistent datetime formats across different character entries

9. **Partial name matching**:
   - Search with "Jan" to verify it returns "Janice Rand" and other Jan-prefix names
   - Test with common surname like "Paris" to verify both Tom Paris and Owen Paris
   - Search with abbreviated names like "Dr." to test prefix handling

10. **API versioning behavior**:
    - Compare responses between /api/v1/rest/character/search and any other available versions
    - Test with explicit version headers if supported
    - Verify deprecated fields (if any documented) are properly handled

