<script setup lang="ts">
import { ref } from "vue";

const API_URL = import.meta.env.VITE_API_URL;
const url = ref("");
const shortUrl = ref("");

async function createShortLink() {
	try {
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
	}
}
</script>

<template>
	<div class="min-h-screen flex items-center justify-center">
		<div class="w-125 p-6 shadow rounded">
			<h1 class="text-2xl font-bold mb-5">Shorten-URL</h1>

			<input
				v-model="url"
				type="text"
				placeholder="Entrer une URL"
				class="border p-2 w-full rounded mb-4"
			/>

			<button
				@click="createShortLink"
				class="bg-blue-500 text-white px-4 py-2 rounded"
			>
				Créer
			</button>

			<div v-if="shortUrl" class="mt-4">
				<p>Lien généré :</p>

				<a :href="shortUrl" target="_blank" class="text-blue-500">
					{{ shortUrl }}
				</a>
			</div>
		</div>
	</div>
</template>
