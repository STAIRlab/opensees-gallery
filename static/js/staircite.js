// staircite.js

// Entry Class: Abstracts the process of getting citation data from CSL JSON
class Entry {
  constructor(entryData) {
    this.entryData = entryData;
  }

  // Extract year from "issued" or "year"
  getYear() {
    if (this.entryData.year) {
      return this.entryData.year; // Direct year field
    }
    if (this.entryData.issued && this.entryData.issued["date-parts"]) {
      return this.entryData.issued["date-parts"][0][0]; // Extract from "issued"
    }
    return null; // No year found
  }

  // Get author names formatted
  getAuthors() {
    if (!this.entryData.author) return '';
    return this.entryData.author.map(a => `${a.given} ${a.family}`).join(", ");
  }

  // Get title of the work
  getTitle() {
    return this.entryData.title || '';
  }

  // Get publisher
  getPublisher() {
    return this.entryData.publisher || '';
  }

  // Get URL if available
  getUrl() {
    return this.entryData.url || '';
  }

  // Get DOI if available
  getDOI() {
    // Assuming your CSL-JSON has a field called "DOI"
    return this.entryData.DOI || '';
  }
}

// Formatter Class: Base class for citation formatters
class Formatter {
  // Abstract method to format a citation (in-text)
  formatCitation(entry, element) {
    throw "formatCitation() must be implemented by a subclass";
  }

  // Abstract method to format the bibliography (full reference)
  formatBibliography(entry, element) {
    throw "formatBibliography() must be implemented by a subclass";
  }

  // Optional helper to generate a full citation string for tooltips
  // (You can override or customize per style if needed.)
  generateFullCitationString(entry) {
    // By default, returns a simple "Author (Year). Title. Publisher. DOI"
    const authors = entry.getAuthors();
    const year = entry.getYear();
    const title = entry.getTitle();
    const publisher = entry.getPublisher();
    const doi = entry.getDOI();

    let fullCitation = `${authors} (${year}). ${title}. ${publisher}`;
    if (doi) {
      fullCitation += `. doi: ${doi}`;
    }
    return fullCitation;
  }
}

// APA Formatter
class APAFormatter extends Formatter {
  // Example In-Text: Author (Year)
  formatCitation(entry, element) {
    const authors = entry.getAuthors();
    const year = entry.getYear();
    const doi = entry.getDOI();

    // Short in-text citation
    const shortCitation = `${authors} (${year})`;

    // Full citation string for tooltip
    const fullCitation = this.generateFullCitationString(entry);

    if (doi) {
      // Make the entire text a link to the DOI, with a tooltip
      element.innerHTML = `<a href="https://doi.org/${doi}" 
                              target="_blank" 
                              title="${fullCitation}">
                              ${shortCitation}
                           </a>`;
    } else {
      // No DOI: just put the short citation, but still add the tooltip
      element.innerHTML = `<span title="${fullCitation}">${shortCitation}</span>`;
    }
  }

  // Example Bibliography: Authors (Year). Title in italics. Publisher. DOI link.
  formatBibliography(entry, element) {
    const authors = entry.getAuthors();
    const year = entry.getYear();
    const title = entry.getTitle();
    const publisher = entry.getPublisher();
    const doi = entry.getDOI();

    let ref = `${authors} (${year}). <i>${title}</i>. ${publisher}.`;

    if (doi) {
      ref += ` <a href="https://doi.org/${doi}" target="_blank">https://doi.org/${doi}</a>`;
    }

    element.innerHTML = ref;
  }
}

// MLA Formatter
class MLAFormatter extends Formatter {
  // Example In-Text: (Author Year) [Very simplified]
  formatCitation(entry, element) {
    const authors = entry.getAuthors();
    const year = entry.getYear();
    const doi = entry.getDOI();

    const shortCitation = `(${authors} ${year})`;
    const fullCitation = this.generateFullCitationString(entry);

    if (doi) {
      element.innerHTML = `<a href="https://doi.org/${doi}" 
                              target="_blank" 
                              title="${fullCitation}">
                              ${shortCitation}
                           </a>`;
    } else {
      element.innerHTML = `<span title="${fullCitation}">${shortCitation}</span>`;
    }
  }

  // Example Bibliography: Authors. Title in italics. Publisher, Year. [DOI link if available]
  formatBibliography(entry, element) {
    const authors = entry.getAuthors();
    const year = entry.getYear();
    const title = entry.getTitle();
    const publisher = entry.getPublisher();
    const doi = entry.getDOI();

    let ref = `${authors}. <i>${title}</i>. ${publisher}, ${year}.`;
    if (doi) {
      ref += ` <a href="https://doi.org/${doi}" target="_blank">https://doi.org/${doi}</a>`;
    }

    element.innerHTML = ref;
  }
}

// Chicago Formatter
class ChicagoFormatter extends Formatter {
  // Example In-Text: Authors Year [Simplified Chicago author-date]
  formatCitation(entry, element) {
    const authors = entry.getAuthors();
    const year = entry.getYear();
    const doi = entry.getDOI();

    const shortCitation = `${authors} ${year}`;
    const fullCitation = this.generateFullCitationString(entry);

    if (doi) {
      element.innerHTML = `<a href="https://doi.org/${doi}" 
                              target="_blank" 
                              title="${fullCitation}">
                              ${shortCitation}
                           </a>`;
    } else {
      element.innerHTML = `<span title="${fullCitation}">${shortCitation}</span>`;
    }
  }

  // Example Bibliography: Authors. Title in italics. Publisher, Year. [DOI link if available]
  formatBibliography(entry, element) {
    const authors = entry.getAuthors();
    const year = entry.getYear();
    const title = entry.getTitle();
    const publisher = entry.getPublisher();
    const doi = entry.getDOI();

    let ref = `${authors}. <i>${title}</i>. ${publisher}, ${year}.`;
    if (doi) {
      ref += ` <a href="https://doi.org/${doi}" target="_blank">https://doi.org/${doi}</a>`;
    }

    element.innerHTML = ref;
  }
}

// CitationManager Class: Manages citations on the page
export class CitationManager {
  constructor(bibliographyUrl, options = {}) {
    this.options = {
      style: 'apa', // Default citation style
      showFullBibliography: false, // Do not show the full bibliography by default
      ...options, // Override default options with user-provided options
    };

    this.bibliographyUrl = bibliographyUrl;
    this.bibliography = [];
    this.citedReferences = new Set();  // Track which references have been cited
    this.formatter = this.getFormatter();
  }

  // Get the appropriate formatter based on the selected style
  getFormatter() {
    if (this.options.style === 'apa') {
      return new APAFormatter();
    } else if (this.options.style === 'mla') {
      return new MLAFormatter();
    } else if (this.options.style === 'chicago') {
      return new ChicagoFormatter();
    }
    return new APAFormatter(); // Default to APA
  }

  // Method to fetch and load the bibliography JSON
  async loadBibliography() {
    try {
      const response = await fetch(this.bibliographyUrl);
      const data = await response.json();
      this.bibliography = data.map(entryData => new Entry(entryData));

      // Once loaded, update citations on the page
      this.updateCitations();

      // Optionally show the full bibliography if configured
      this.displayBibliography();
    } catch (error) {
      console.error('Error loading bibliography:', error);
    }
  }

  // Method to update all <cite> elements with the correct citation text
  updateCitations() {
    // Look for both single-key and multi-key attributes
    const cites = document.querySelectorAll("cite[key], cite[keys]");
    cites.forEach(cite => {
      let keyAttr = cite.getAttribute("key");
      let keysAttr = cite.getAttribute("keys");

      // Gather all the keys we need to cite
      let keys = [];
      if (keysAttr) {
        keys = keysAttr.split(",").map(k => k.trim());
      } else if (keyAttr) {
        keys = [keyAttr.trim()];
      }

      // If no keys, skip
      if (!keys.length) return;

      // For each key, find its corresponding entry and generate citation
      const citationStrings = [];
      keys.forEach(k => {
        const entry = this.bibliography.find(item => item.entryData.id === k);
        if (entry) {
          // Mark the reference as cited
          this.citedReferences.add(k);

          // We create a temporary element, let the formatter fill it,
          // then collect the string. This prevents overwriting each other.
          const tempSpan = document.createElement('span');
          this.formatter.formatCitation(entry, tempSpan);
          citationStrings.push(tempSpan.innerHTML);
        }
      });

      // Join multiple citations with a semicolon (or any delimiter you prefer)
      cite.innerHTML = citationStrings.join("; ");
    });
  }

  // Method to display the full bibliography (if requested)
  displayBibliography() {
    const bibliographyList = document.getElementById('bibliography-list');
    if (!bibliographyList) return;  // If there's no <ul> or <ol> with that ID, skip

    this.bibliography.forEach(entry => {
      // Only show cited references (those with a matching key in citedReferences)
      // unless the user wants the full bibliography displayed
      if (this.options.showFullBibliography || this.citedReferences.has(entry.entryData.id)) {
        const li = document.createElement('li');
        this.formatter.formatBibliography(entry, li);
        bibliographyList.appendChild(li);
      }
    });
  }
}

