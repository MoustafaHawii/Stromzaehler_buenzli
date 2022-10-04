/**
 * Downloads a file with a text content
 * @param {string} filename the filename
 * @param {string} text the text content
 */
function download(filename, text) {
	const element = document.createElement("a");
	element.setAttribute(
		"href",
		"data:text/plain;charset=utf-8," + encodeURIComponent(text)
	);

	element.setAttribute("download", filename);
	element.style.display = "none";

	document.body.appendChild(element);

	element.click();
	document.body.removeChild(element);
}

/**
 * Converts JSON data to CSV
 * @param {Object} json
 * @returns converted csv
 */
function jsonToCSV(json) {
	let output =
		"timestamp;realtive feed; absolute feed;relative usage; absolute usage";
	for (const entry of json) {
		const { ts, feedR, feedA, usgR, usgA } = entry;
		output += `\n${ts};${feedR};${feedA};${usgR};${usgA}`;
	}
	return output;
}
