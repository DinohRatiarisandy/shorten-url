import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		path: "/",
		component: () => import("@/views/Home.vue"),
	},

	{
		path: "/admin/login",
		component: () => import("@/admin/components/AdminLogin.vue"),
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
