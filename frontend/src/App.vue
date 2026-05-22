<script setup lang="ts">
import { ref } from "vue";
import QrCode from "./components/QrCode.vue";
import { HalfCircleSpinner } from "epic-spinners";

const API_URL = import.meta.env.VITE_API_URL;

const url = ref("");
const shortUrl = ref("");
const loading = ref(false);
const copied = ref(false);
const errorMessage = ref("");

function validationUrl(url: string) {
	return url.startsWith("http://") || url.startsWith("https://");
}

async function createShortLink() {
	errorMessage.value = "";

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

		if (!url.value || !url.value.startsWith("http")) {
			alert("URL invalide (doit commencer par http)");
			return;
		}

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

		shortUrl.value = `${API_URL}/${data.short_code}`;
	} catch (error) {
		console.log(error);
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

			<!-- Input -->
			<section>
				<input
					v-model="url"
					@input="errorMessage = ''"
					type="text"
					placeholder="Entrer une URL (https://...)"
					class="border p-3 w-full rounded-lg mb-4 outline-none focus:ring-2 focus:ring-blue-400"
				/>
				<p
					v-if="errorMessage"
					class="text-red-500 text-sm animate-pulse mb-2"
				>
					⚠️ {{ errorMessage }}
				</p>
			</section>

			<!-- Button -->
			<button
				@click="createShortLink"
				:disabled="loading || !url"
				class="w-full bg-blue-500 text-white py-2 rounded-lg flex items-center justify-center gap-2 disabled:opacity-50"
			>
				<!-- Loading state -->
				<span v-if="loading" class="flex items-center gap-2">
					<half-circle-spinner
						:animation-duration="1000"
						:size="18"
						color="#ffffff"
					/>
					<span>Generating...</span>
				</span>

				<!-- Default state -->
				<span v-else>Create a link</span>
			</button>
			<p
				v-if="loading"
				class="text-xs text-gray-600 mt-2 text-center animate-pulse"
			>
				⏳ Be patient 😄 I'm using free hosting, so my backend may take
				a few seconds to wake up...
			</p>

			<!-- Result -->
			<div v-if="shortUrl" class="mt-6">
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
