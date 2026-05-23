import { ref } from "vue";
import { createShortLink } from "@/services/linkService";
import { isValidUrl, getHostname } from "@/utils/urlHelper";
import { API_HOSTNAME } from "@/services/linkService";

export function useUrlShortener() {
	const url = ref("");
	const shortUrl = ref("");
	const loading = ref(false);
	const errorMessage = ref("");
	const lastSubmittedUrl = ref("");
	const customCode = ref("");

	async function submit() {
		errorMessage.value = "";

		if (getHostname(url.value) == API_HOSTNAME) {
			errorMessage.value =
				"You can't shorten an already shortened link. 😒";
			return;
		}
		if (!url.value) {
			errorMessage.value = "Please enter a URL.";
			return;
		}
		if (!isValidUrl(url.value)) {
			errorMessage.value = "Invalid URL.";
		}
		if (url.value === lastSubmittedUrl.value) {
			errorMessage.value = "This url was already shortened";
			return;
		}

		try {
			loading.value = true;
			errorMessage.value = "";
			shortUrl.value = await createShortLink(url.value, customCode.value);
			lastSubmittedUrl.value = url.value;
		} catch (error: any) {
			errorMessage.value = error.message || "Network error.";
		} finally {
			loading.value = false;
		}
	}

	function clearInput() {
		url.value = "";
		errorMessage.value = "";
		customCode.value = "";
	}

	return {
		url,
		customCode,
		shortUrl,
		loading,
		errorMessage,
		lastSubmittedUrl,
		submit,
		clearInput,
	};
}
