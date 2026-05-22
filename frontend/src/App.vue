<script setup lang="ts">
import { ref } from "vue";
import QrCode from "./components/QrCode.vue";

const API_URL = import.meta.env.VITE_API_URL;
const API_HOSTNAME = new URL(API_URL).hostname;

const url = ref("");
const shortUrl = ref("");
const loading = ref(false);
const copied = ref(false);
const errorMessage = ref("");
const lastSubmittedUrl = ref("");

function getHostname(url: string) {
	try {
		return new URL(url).hostname;
	} catch {
		return null;
	}
}

function validationUrl(url: string) {
	return url.startsWith("http://") || url.startsWith("https://");
}

function clearInput() {
	errorMessage.value = "";
	url.value = "";
}

function onInputChange() {
	errorMessage.value = "";
	lastSubmittedUrl.value = "";
}

async function createShortLink() {
	errorMessage.value = "";
	const inputHost = getHostname(url.value);

	if (inputHost === API_HOSTNAME) {
		errorMessage.value =
			"You can't shorten a link that's already shortened. 😅";
		return;
	}

	if (loading.value) return;

	if (url.value === lastSubmittedUrl.value && shortUrl.value) {
		errorMessage.value = "This URL was already shortened";
	}

	if (!url.value) {
		errorMessage.value = "Please enter a valid URL";
		return;
	}

	if (!validationUrl(url.value)) {
		errorMessage.value =
			"Invalid URL (must start with http:// or https://)";
		return;
	}

	try {
		loading.value = true;
		copied.value = false;

		const response = await fetch(`${API_URL}/links/`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				original_url: url.value,
			}),
		});

		const data = await response.json();

		if (!response.ok) {
			errorMessage.value = data.detail || "Server error";
			return;
		}

		shortUrl.value = `${API_URL}/${data.short_code}`;
		lastSubmittedUrl.value = url.value;
	} catch (error) {
		errorMessage.value = "Network error";
	} finally {
		loading.value = false;
	}
}

function copyToClipboard() {
	if (!shortUrl.value) return;

	navigator.clipboard.writeText(shortUrl.value);
	copied.value = true;

	setTimeout(() => {
		copied.value = false;
	}, 1500);
}
</script>

<template>
	<div class="min-h-screen flex items-center justify-center bg-gray-50">
		<div class="w-105 p-6 shadow-xl rounded-2xl bg-white">
			<!-- Title -->
			<h1 class="text-2xl font-bold mb-6 text-center">Shorten URL 🚀</h1>
			<form @submit.prevent="createShortLink">
				<!-- Input -->
				<div class="relative">
					<input
						v-model="url"
						@input="errorMessage = ''"
						type="text"
						placeholder="Entrer une URL (https://...)"
						class="border p-3 w-full rounded-lg mb-4 outline-none focus:ring-2 focus:ring-blue-400"
					/>
					<!-- Clear button -->
					<button
						v-if="url"
						type="button"
						@click="clearInput"
						class="absolute right-1 top-3.75 -translate-y-1/2 text-gray-400 hover:text-red-500"
						title="Clear"
					>
						✖
					</button>
				</div>
				<p
					v-if="errorMessage"
					class="text-red-500 text-sm animate-pulse mb-2"
				>
					⚠️ {{ errorMessage }}
				</p>

				<!-- Button -->
				<button
					type="submit"
					:disabled="loading || !url || lastSubmittedUrl === url"
					class="w-full bg-blue-500 text-white py-2 rounded-lg flex items-center justify-center gap-2 disabled:opacity-50"
				>
					<!-- Loading state -->
					<span v-if="loading" class="flex items-center gap-2">
						<span
							class="animate-spin border-2 border-white border-t-transparent rounded-full w-4 h-4"
						></span>
						<span>Generating...</span>
					</span>

					<!-- Default state -->
					<span v-else>Create a link</span>
				</button>
				<p
					v-if="loading"
					class="text-xs text-gray-600 mt-2 text-center animate-pulse"
				>
					⏳ Be patient 😄 I'm using free hosting, so my backend may
					take a few seconds to wake up...
				</p>
			</form>
			<!-- Result -->
			<div v-if="shortUrl && !loading" class="mt-6">
				<p class="mb-2 font-medium">Link generated :</p>

				<div class="flex items-center gap-2 bg-gray-100 p-3 rounded-lg">
					<a
						:href="shortUrl"
						target="_blank"
						class="text-blue-600 break-all flex-1"
					>
						{{ shortUrl }}
					</a>

					<!-- Copy button -->
					<button
						@click="copyToClipboard"
						class="p-2 hover:bg-gray-200 rounded-lg transition"
						title="Copier"
					>
						📋
					</button>
				</div>

				<!-- Copied message -->
				<p v-if="copied" class="text-green-500 text-sm mt-2">
					Copied ✔
				</p>
			</div>

			<!-- QR Code -->
			<div v-if="shortUrl && !loading" class="mt-6 flex justify-center">
				<QrCode :url="shortUrl" />
			</div>
		</div>
	</div>
</template>
