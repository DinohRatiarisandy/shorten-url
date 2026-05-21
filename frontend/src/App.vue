<script setup lang="ts">
import { ref } from "vue";
import QrCode from "./components/QrCode.vue";

const API_URL = import.meta.env.VITE_API_URL;

const url = ref("");
const shortUrl = ref("");
const loading = ref(false);
const copied = ref(false);

async function createShortLink() {
	if (!url.value) return;

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
			<input
				v-model="url"
				type="text"
				placeholder="Entrer une URL (https://...)"
				class="border p-3 w-full rounded-lg mb-4 outline-none focus:ring-2 focus:ring-blue-400"
			/>

			<!-- Button -->
			<button
				@click="createShortLink"
				:disabled="loading || !url"
				class="w-full bg-blue-500 text-white py-2 rounded-lg flex items-center justify-center gap-2 disabled:opacity-50"
			>
				<span v-if="loading">⏳ Génération...</span>
				<span v-else>Créer un lien</span>
			</button>

			<!-- Result -->
			<div v-if="shortUrl" class="mt-6">
				<p class="mb-2 font-medium">Lien généré :</p>

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
