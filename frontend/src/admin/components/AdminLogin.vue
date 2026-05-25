<script setup>
import { loginAdmin } from "@/admin/services/admin.api";
import { useRouter } from "vue-router";
import { ref } from "vue";

const router = useRouter();

const email = ref("");
const password = ref("");

const errorMessage = ref("");
const loading = ref(false);

const handleLogin = async () => {
	if (!email.value || !password.value) return;

	errorMessage.value = "";
	loading.value = true;

	try {
		await loginAdmin(email.value, password.value);

		router.push("/");
	} catch (error) {
		if (error instanceof Error) {
			errorMessage.value = error.message;
		} else {
			errorMessage.value = "Something went wrong";
		}
	} finally {
		loading.value = false;
	}
};
</script>

<template>
	<form
		@submit.prevent="handleLogin"
		class="h-screen flex flex-col justify-center items-center"
	>
		<h1 class="text-2xl">Log In</h1>
		<div v-if="errorMessage" class="text-red-500 text-sm mt-2">
			{{ errorMessage }}
		</div>
		<div class="flex flex-col">
			<div>
				<label for="email">Email:</label>
				<input
					v-model="email"
					class="p-2 outline-none"
					type="email"
					placeholder="email@domain.com"
					id="email"
				/>
			</div>
			<div>
				<label for="password">Password:</label>
				<input
					v-model="password"
					class="p-2 outline-none"
					type="password"
					placeholder="password"
					id="password"
				/>
			</div>
			<button
				:disabled="!email || !password"
				type="submit"
				class="cursor-pointer w-full bg-blue-500 text-white py-2 rounded-lg flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
			>
				Log In
			</button>
		</div>
	</form>
</template>
