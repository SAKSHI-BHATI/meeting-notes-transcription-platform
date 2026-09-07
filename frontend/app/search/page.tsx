import Link from "next/link";
import { Sidebar } from "@/components/sidebar";
export default function SearchPage(){return <div className="shell"><Sidebar/><main className="content"><p className="eyebrow">DISCOVER</p><h1>Search</h1><p className="subtle">Use the meeting library search to find conversations by title or participant.</p><Link className="primary" href="/">Go to meetings</Link></main></div>}
