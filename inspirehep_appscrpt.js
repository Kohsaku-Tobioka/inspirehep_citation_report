var authorId = "K.Tobioka.1";
var authorName = "Tobioka, K.";
var pastDays = 7; 
var emailAddress = "ktobioka@fsu.edu";





function main(inputAuthorId, inputAuthorName, inputPastDays, inputEmailAddress) {
    // Use provided values or default ones
    //authorId = inputAuthorId || authorId0;
    authorName = inputAuthorName || authorName;
    pastDays = inputPastDays || pastDays;
    emailAddress = inputEmailAddress || emailAddress;

    const url = createQueryUrl(authorId, 100, pastDays);
    console.log(url)
    const result = fetchInspirehepPapers(url);
    const jsonDict = JSON.parse(result);
    const references = jsonDict.hits.hits;
    
    const message = processReferences(references, authorName, pastDays);
    sendEmails(message, emailAddress);
}


function sendEmails(message, emailAddress) {
    var subject = 'Inspire Citation Report';
    MailApp.sendEmail(emailAddress, subject, message, {
      body: message,
    });
}

function createQueryUrl(authorIdentifier, maxResults = 10, pastDays = 7, page = 1, sortOrder = 'mostrecent') {
    const currentDate = new Date();
    currentDate.setDate(currentDate.getDate() - pastDays);
    const dayStart = `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${currentDate.getDate().toString().padStart(2, '0')}`;
        
    const params = {
        q: `de > ${dayStart} and refersto:author:${authorIdentifier}`,
        size: maxResults,
        page: page,
        sort: sortOrder
    };

    const queryString = Object.keys(params)
                              .map(key => `${key}=${encodeURIComponent(params[key])}`)
                              .join('&');
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


function processReferences(references, authorName, pastDays) {
    let output = `Number of citations are ${references.length} in the last ${pastDays} days.\n\n`;

    references.forEach((reference, index) => {
        const title = reference.metadata.titles[0].title;
        const id = reference.id;
        output += `\n[Citation ${index + 1}]\n`;
        output += `Title: ${title}\n`;

        if (reference.metadata.authors) {
            const authorFullNames = reference.metadata.authors.map(author => author.full_name);
            output += `Authors: ${authorFullNames.join(',  ')}\n`;  // Note the two spaces after the comma
        } else if (reference.metadata.corporate_author) {
            output += `Corporate_author: ${reference.metadata.corporate_author}\n`;
        } else {
            output += 'Keys: authors/corporate_author not found\n';
        }

        output += `Link: https://inspirehep.net/literature/${id}`+ '\n \n';

        const citedRefs = readoutCitedPaper(reference, authorName);

        if (citedRefs.length === 0) {
            output += `Cited ref: ${authorName} not found. Possibly a big collaboration paper.\n`;
        } else {
            output += `Cited ref: ${citedRefs.join(', ')}\n`;
        }
    });

    return output;
}



