<script setup lang="ts">
import { ref } from "vue";
import UrlInput from "@/components/UrlInput.vue";
import QrCode from "@/components/QrCode.vue";
import ShortUrlResult from "@/components/ShortUrlResult.vue";
import { useUrlShortener } from "@/composables/useUrlShortener";

const copied = ref(false);
const {
	url,
	customCode,
	shortUrl,
	loading,
	errorMessage,
	lastSubmittedUrl,
	submit,
	clearInput,
} = useUrlShortener();

function copyToClipboard(text: string) {
	navigator.clipboard.writeText(text);
	copied.value = true;

	setTimeout(() => {
		copied.value = false;
	}, 1500);
}

function onInputChange() {
	errorMessage.value = "";
	lastSubmittedUrl.value = "";
}
</script>

<template>
	<router-view />
	<div class="min-h-screen flex items-center justify-center bg-gray-50">
		<div class="w-105 p-6 shadow-xl rounded-2xl bg-white">
			<!-- Title -->
			<h1 class="text-2xl font-bold mb-6 text-center">Shorten URL 🚀</h1>
			<!-- URL input -->
			<UrlInput
				v-model="url"
				v-model:customCode="customCode"
				:loading="loading"
				:error="errorMessage"
				:disabled="lastSubmittedUrl === url"
				@submit="submit"
				@clear="clearInput"
				@change="onInputChange"
				@update:customCode="customCode = $event"
			/>

			<!-- Result -->
			<ShortUrlResult
				:shortUrl="shortUrl"
				:loading="loading"
				:copied="copied"
				@copyToClipboard="copyToClipboard"
			/>

			<!-- QR Code -->
			<div v-if="shortUrl && !loading" class="mt-6 flex justify-center">
				<QrCode :url="shortUrl" />
			</div>
		</div>
	</div>
</template>
