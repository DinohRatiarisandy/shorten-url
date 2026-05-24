<script setup lang="ts">
import { ref, nextTick, useTemplateRef } from "vue";
import { API_URL } from "@/services/linkService";

const showCustomCodeInput = ref(false);
const customCodeInput = useTemplateRef("customCodeInput");

const props = defineProps<{
	modelValue: string; // v-model='url'
	customCode: string;
	loading: boolean;
	error: string;
	disabled: boolean;
}>();

const emit = defineEmits<{
	"update:modelValue": [value: string];
	"update:customCode": [value: string];
	submit: [];
	clear: [];
	change: [];
}>();

function handleInput(event: Event) {
	const value = (event.target as HTMLInputElement).value;
	emit("update:modelValue", value);
	emit("change");
}

async function handleCustomCode() {
	showCustomCodeInput.value = !showCustomCodeInput.value;

	if (showCustomCodeInput.value) {
		await nextTick();
		customCodeInput.value?.focus();
	} else {
		emit("update:customCode", "");
	}
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
			<p
				@click="handleCustomCode"
				class="cursor-pointer text-sm text-gray-700 mb-1 font-semibold"
			>
				🛠️Customize my URL
			</p>
			<!-- Custom Code -->
			<div
				v-if="showCustomCodeInput"
				class="flex items-center rounded-lg px-3 py-2 mb-4"
			>
				<label
					for="custom-code-input"
					class="text-gray-400 text-sm whitespace-nowrap"
					>{{ API_URL }}/</label
				>
				<input
					ref="customCodeInput"
					:value="props.customCode"
					@input="
						emit(
							'update:customCode',
							($event.target as HTMLInputElement).value,
						)
					"
					type="text"
					placeholder="custom-alias"
					class="outline-none text-sm flex-1 min-w-0"
					id="custom-code-input"
					maxlength="15"
				/>
			</div>
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
