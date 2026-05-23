<script setup lang="ts">
const props = defineProps<{
	modelValue: string; // v-model='url'
	loading: boolean;
	error: string;
	disabled: boolean;
}>();

const emit = defineEmits<{
	"update:modelValue": [value: string];
	submit: [];
	clear: [];
	change: [];
}>();

function handleInput(event: Event) {
	const value = (event.target as HTMLInputElement).value;
	emit("update:modelValue", value);
	emit("change");
}
</script>

<template>
	<form @submit.prevent="emit('submit')">
		<!-- Input -->
		<div class="relative">
			<input
				:value="props.modelValue"
				@input="handleInput"
				type="text"
				placeholder="Entrer une URL (https://...)"
				class="border p-3 w-full rounded-lg mb-4 outline-none focus:ring-2 focus:ring-blue-400"
			/>
			<!-- Clear button -->
			<button
				v-if="props.modelValue"
				type="button"
				@click="emit('clear')"
				class="absolute right-1 top-3.75 -translate-y-1/2 text-gray-400 hover:text-red-500"
				title="Clear"
			>
				✖
			</button>
		</div>
		<p v-if="props.error" class="text-red-500 text-sm animate-pulse mb-2">
			⚠️ {{ props.error }}
		</p>

		<!-- Button -->
		<button
			type="submit"
			:disabled="props.disabled || props.loading || !props.modelValue"
			class="w-full bg-blue-500 text-white py-2 rounded-lg flex items-center justify-center gap-2 disabled:opacity-50"
		>
			<!-- Loading state -->
			<span v-if="props.loading" class="flex items-center gap-2">
				<span
					class="animate-spin border-2 border-white border-t-transparent rounded-full w-4 h-4"
				></span>
				<span>Generating...</span>
			</span>

			<!-- Default state -->
			<span v-else>Create a link</span>
		</button>
		<p
			v-if="props.loading"
			class="text-xs text-gray-600 mt-2 text-center animate-pulse"
		>
			⏳ Be patient 😄 I'm using free hosting, so my backend may take a
			few seconds to wake up...
		</p>
	</form>
</template>
