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

const json = [
	{
		ts: 2163478,
		feedR: 1.2,
		feedA: 4567,
		usgR: 0.9,
		usgA: 5678,
	},
	{
		ts: 34567888,
		feedR: 1.4,
		feedA: 2349,
		usgR: 0.1,
		usgA: 283459,
	},
	{
		ts: 456789436,
		feedR: 1.2,
		feedA: 45235,
		usgR: 0.9,
		usgA: 235,
	},
];

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
