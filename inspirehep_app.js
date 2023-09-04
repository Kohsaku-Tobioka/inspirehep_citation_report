
function createQueryUrl(authorIdentifier, maxResults = 10, page = 1, sortOrder = 'mostrecent', pastDays = 7) {
    const currentDate = new Date();
    currentDate.setDate(currentDate.getDate() - pastDays);
    const dayStart = `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${currentDate.getDate().toString().padStart(2, '0')}`;
    
    const params = {
        q: `de+%3E+${dayStart}+and+refersto%3Aauthor%3A${authorIdentifier}`,
        size: maxResults,
        page: page,
        sort: sortOrder
    };

    const queryString = Object.keys(params).map(key => key + '=' + params[key]).join('&');
    const base_url = 'https://inspirehep.net/api/literature?';

    return base_url + queryString;
}

function fetchInspirehepPapers(url) {
    const response = UrlFetchApp.fetch(url);
    if (response.getResponseCode() !== 200) {
        throw new Error(`Failed to fetch papers: ${response.getResponseCode()}`);
    }
    return response.getContentText();
}

function extractAuthorNamesFromReference(reference) {
    return reference.reference.authors.map(author => author.full_name);
}

function readoutCitedPaper(reference, name) {
    const outputMyref = [];
    for (let ref of reference.metadata.references) {
        if (ref.reference && ref.reference.authors) {
            if (extractAuthorNamesFromReference(ref).includes(name)) {
                if (ref.reference.title) {
                    outputMyref.push(`[${ref.reference.label}]`);
                    outputMyref.push(ref.reference.title.title);
                } else if (ref.raw_refs) {
                    outputMyref.push(ref.raw_refs[0].value);
                } else {
                    outputMyref.push("Reference title or raw_refs not found");
                }
            }
        }
    }
    return outputMyref;
}

function processReferences(references, authorName) {
    Logger.log(`Number of citations are ${references.length} in the last 7 days`);

    references.forEach((reference, index) => {
        const title = reference.metadata.titles[0].title;
        const id = reference.id;
        Logger.log(`\nRef${index + 1}`);
        Logger.log(`Title: ${title}`);
        Logger.log(`Link: https://inspirehep.net/literature/${id}`);

        if (reference.metadata.authors) {
            const authorFullNames = reference.metadata.authors.map(author => author.full_name);
            Logger.log(`Authors: ${authorFullNames}`);
        } else if (reference.metadata.corporate_author) {
            Logger.log(`Corporate_author: ${reference.metadata.corporate_author}`);
        } else {
            Logger.log('Keys: authors/corporate_author not found');
        }

        const citedRefs = readoutCitedPaper(reference, authorName);

        if (citedRefs.length === 0) {
            Logger.log(`Cited ref: ${authorName} not found. Possibly a big collaboration paper.`);
        } else {
            Logger.log(`Cited ref: ${citedRefs.join(', ')}`);
        }
    });
}

function main() {
    const authorId = "K.Tobioka.1";
    const authorName = "Tobioka, K.";
    const url = createQueryUrl(authorId, 100);
    console.log(url)
    const result = fetchInspirehepPapers(url);
    const jsonDict = JSON.parse(result);
    const references = jsonDict.hits.hits;
    processReferences(references, authorName);
}

