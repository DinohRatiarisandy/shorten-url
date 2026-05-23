const API_URL = import.meta.env.VITE_API_URL;
export const API_HOSTNAME = new URL(API_URL).hostname;

export async function createShortLink(original_url: string) {
	const response = await fetch(`${API_URL}/links/`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			original_url: original_url,
		}),
	});

	const data = await response.json();
	if (!response.ok) throw new Error(data.detail || "Server Error !");
	return `${API_URL}/${data.short_code}`;
}
