export function getHostname(url: string) {
	try {
		return new URL(url).hostname;
	} catch {
		return null;
	}
}

export function isValidUrl(url: string) {
	return url.startsWith("http://") || url.startsWith("https://");
}
