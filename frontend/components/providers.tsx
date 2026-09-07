"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createContext, useContext, useEffect, useState } from "react";

type Theme = "light" | "dark";
const ThemeContext = createContext<{theme: Theme; toggleTheme: () => void} | null>(null);

export function useTheme(){const context=useContext(ThemeContext);if(!context)throw new Error("useTheme must be used within Providers");return context;}

export function Providers({children}:{children:React.ReactNode}) { const [client] = useState(() => new QueryClient({defaultOptions:{queries:{staleTime:20_000, retry:1}}})); const [theme,setTheme]=useState<Theme>("light"); const [mounted,setMounted]=useState(false); useEffect(()=>{const saved=window.localStorage.getItem("recall-theme");if(saved==="dark"||saved==="light")setTheme(saved);setMounted(true)},[]);useEffect(()=>{if(!mounted)return;document.documentElement.dataset.theme=theme;window.localStorage.setItem("recall-theme",theme)},[theme,mounted]);const toggleTheme=()=>setTheme(current=>current==="dark"?"light":"dark");return <QueryClientProvider client={client}><ThemeContext.Provider value={{theme,toggleTheme}}>{children}</ThemeContext.Provider></QueryClientProvider>; }
