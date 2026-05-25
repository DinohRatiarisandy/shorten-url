const BASE_URL = import.meta.env.VITE_API_URL;

export async function apiFetch(url: string, options: RequestInit = {}) {
	return fetch(`${BASE_URL}${url}`, {
		...options,
		credentials: "include",
		headers: {
			"Content-Type": "application/json",
			...(options.headers || {}),
		},
	});
}
