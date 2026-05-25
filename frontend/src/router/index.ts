import { createRouter, createWebHistory } from "vue-router";
import { getMe } from "@/admin/services/auth";

const routes = [
	{
		path: "/",
		component: () => import("@/views/Home.vue"),
	},

	{
		path: "/admin/login",
		component: () => import("@/admin/components/AdminLogin.vue"),
	},

	{
		path: "/admin/dashboard",
		component: () => import("@/admin/components/AdminDashboard.vue"),
		meta: { requiresAuth: true },
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

router.beforeEach(async (to) => {
	if (to.meta.requiresAuth) {
		try {
			await getMe();
			return true;
		} catch {
			return "/admin/login";
		}
	}

	return true;
});

export default router;
