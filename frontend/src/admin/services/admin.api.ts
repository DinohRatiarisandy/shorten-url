import { apiFetch } from "@/api/fetchClient";

export async function loginAdmin(email: string, password: string) {
	const response = await apiFetch("/auth/login", {
		method: "POST",
		body: JSON.stringify({
			email,
			password,
		}),
	});

	const raw = await response.text();

	let data;
	try {
		data = JSON.parse(raw);
	} catch {
		throw new Error("Server returned invalid response");
	}

	if (!response.ok) {
		throw new Error(data.detail || "Login failed");
	}

	return data;
}
