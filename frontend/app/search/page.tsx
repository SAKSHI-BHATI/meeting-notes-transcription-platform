"use client";
import Link from "next/link";
import { Search } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { Sidebar } from "@/components/sidebar";
import { useDebounce } from "@/hooks/use-debounce";
import { api } from "@/services/api";
import { formatDate, formatDuration } from "@/lib/time";
import { useState } from "react";

export default function SearchPage(){const [value,setValue]=useState("");const query=useDebounce(value.trim(),300);const result=useQuery({queryKey:["global-search",query],queryFn:()=>api.search(query),enabled:query.length>0});return <div className="shell"><Sidebar/><main className="content"><p className="eyebrow">DISCOVER</p><h1>Search everything</h1><p className="subtle">Find meetings, people, and words spoken in transcripts.</p><label className="global-search"><Search size={20}/><input autoFocus value={value} onChange={event=>setValue(event.target.value)} placeholder="Search meetings, people, or transcript content"/></label>{!query&&<div className="empty">Start typing to search across your workspace.</div>}{result.isLoading&&<div className="empty">Searching conversations…</div>}{result.isError&&<div className="empty">Search is unavailable right now. Try again.</div>}{result.data&&<section className="search-results"><p className="library-meta"><b>{result.data.items.length} results</b><span>for “{query}”</span></p>{result.data.items.map((item,index)=><Link className="search-result" href={`/meetings/${item.meeting_id}${item.start_time_ms!==null?`?at=${item.start_time_ms}`:""}`} key={`${item.type}-${item.meeting_id}-${item.start_time_ms??index}`}><span className={`result-type ${item.type}`}>{item.type === "transcript" ? "Transcript" : "Meeting"}</span><div><h3>{item.meeting_title}</h3><p>{formatDate(item.occurred_at)} · {item.participant_names.join(", ") || item.speaker_name || "Transcript match"}</p><p className="result-snippet">{item.start_time_ms!==null&&<b>{formatDuration(item.start_time_ms)} · </b>}{item.snippet}</p></div></Link>)}{!result.data.items.length&&<div className="empty">No meetings or transcript passages match “{query}”.</div>}</section>}</main></div>}
