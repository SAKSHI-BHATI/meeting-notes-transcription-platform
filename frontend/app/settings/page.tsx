"use client";
import { Sidebar } from "@/components/sidebar";
import { ThemeToggle } from "@/components/theme-toggle";
export default function SettingsPage(){return <div className="shell"><Sidebar/><main className="content"><p className="eyebrow">WORKSPACE</p><h1>Settings</h1><section className="settings-card"><div><h2>Appearance</h2><p>Choose the workspace color theme that feels right for you.</p></div><ThemeToggle/></section></main></div>}
