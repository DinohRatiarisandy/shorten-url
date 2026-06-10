import { apiFetch } from "@/api/fetchClient";
import type { Link } from "@/types/links";

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

export async function getAdminLinks(): Promise<Link[]> {
    const response = await apiFetch("/admin/links", {
        method: "GET",
        credentials: "include",
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Failed to fetch links");
    }

    return data;
}

export async function deleteAdminLink(id: number) {
    const response = await apiFetch(`/admin/links/${id}`, {
        method: "DELETE",
        credentials: "include",
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.detail || "Failed to delete link");
    }
}

export async function logoutAdmin() {
    const response = await apiFetch("/auth/logout", {
        method: "POST",
        credentials: "include",
    });

    if (!response.ok) {
        throw new Error("Logout failed");
    }

    return await response.json();
}
