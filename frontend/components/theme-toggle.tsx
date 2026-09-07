"use client";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "./providers";

export function ThemeToggle(){const {theme,toggleTheme}=useTheme();const isDark=theme==="dark";return <button className="theme-toggle" onClick={toggleTheme} aria-label={`Switch to ${isDark?"light":"dark"} mode`} title={`Switch to ${isDark?"light":"dark"} mode`}>{isDark?<Sun size={17}/>:<Moon size={17}/>}<span>{isDark?"Light mode":"Dark mode"}</span></button>}
