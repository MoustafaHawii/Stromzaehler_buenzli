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

// ---- Toasts ---------------------------------------------------------------------------

function wait(ms) {
	return new Promise((resolve) => {
		setTimeout(resolve, ms);
	});
}

const toasts = document.querySelector(".toasts").children;
for (let i = 0; i < toasts.length; i++) {
	const toast = toasts[i];
	wait(100 * i).then(() => {
		console.log(toast);
		toast.animate(
			[
				{ transform: "translateY(-100px)", opacity: 1 },
				{
					transform: `translateY(${50 * (toasts.length - i - 1)}px)`,
					opacity: 1,
				},
			],
			{
				fill: "forwards",
				duration: 1000,
			}
		);
		wait(3000 + i * 500).then(() => {
			toast.animate([{}, { opacity: 0 }], {
				fill: "forwards",
				duration: 500,
			});
		});
	});
}
