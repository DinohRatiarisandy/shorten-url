import { apiFetch } from "@/api/fetchClient";

export async function getMe() {
	const res = await apiFetch("/auth/me", {
		method: "GET",
		credentials: "include",
	});

	if (!res.ok) {
		throw new Error("Not authenticated");
	}

	return res.json();
}
