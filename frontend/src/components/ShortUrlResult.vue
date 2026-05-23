<script setup lang="ts">
const props = defineProps<{
	shortUrl: string;
	loading: boolean;
	copied: boolean;
}>();

const emit = defineEmits<{ copyToClipboard: [value: string] }>();
</script>

<template>
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
				@click="emit('copyToClipboard', shortUrl)"
				class="p-2 hover:bg-gray-200 rounded-lg transition"
				title="Copy"
			>
				📋
			</button>
		</div>

		<!-- Copied message -->
		<p v-if="props.copied" class="text-green-500 text-sm mt-2">Copied ✔</p>
	</div>
</template>
