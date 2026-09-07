import { ActionItem, GlobalSearchResult, Meeting, Segment, Summary, Topic } from "@/types";
const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";
async function request<T>(path:string, init?:RequestInit):Promise<T> { const res=await fetch(`${BASE}${path}`,{...init,headers:{"Content-Type":"application/json",...(init?.headers ?? {})}}); if(!res.ok){const error=await res.json().catch(()=>null);throw new Error(error?.error?.message ?? "Something went wrong");} return res.status===204 ? undefined as T : res.json(); }
export const api = {
 meetings:(params:URLSearchParams)=>request<{items:Meeting[];total:number;page:number;page_size:number}>(`/meetings?${params}`),
 search:(query:string)=>request<{query:string;items:GlobalSearchResult[]}>(`/search?q=${encodeURIComponent(query)}`),
 meeting:(id:number)=>request<Meeting>(`/meetings/${id}`),
 transcript:(id:number,q?:string)=>request<{meeting_id:number;items:Segment[]}>(`/meetings/${id}/transcript${q ? `?q=${encodeURIComponent(q)}` : ""}`),
 summary:(id:number)=>request<Summary>(`/meetings/${id}/summary`), topics:(id:number)=>request<Topic[]>(`/meetings/${id}/topics`),
 actions:(id:number)=>request<ActionItem[]>(`/meetings/${id}/action-items`),
 createAction:(id:number,p:Partial<ActionItem>)=>request<ActionItem>(`/meetings/${id}/action-items`,{method:"POST",body:JSON.stringify(p)}),
 updateAction:(id:number,p:Partial<ActionItem>)=>request<ActionItem>(`/action-items/${id}`,{method:"PATCH",body:JSON.stringify(p)}),
 deleteAction:(id:number)=>request<void>(`/action-items/${id}`,{method:"DELETE"}),
 createMeeting:(p:{title:string;occurred_at:string;duration_ms:number;participant_names:string[];transcript_text?:string})=>request<Meeting>("/meetings",{method:"POST",body:JSON.stringify(p)}),
 updateMeeting:(id:number,p:Partial<Meeting>&{participant_names?:string[]})=>request<Meeting>(`/meetings/${id}`,{method:"PATCH",body:JSON.stringify(p)}),
 deleteMeeting:(id:number)=>request<void>(`/meetings/${id}`,{method:"DELETE"}),
 uploadTranscript:async(id:number,file:File)=>{const form=new FormData();form.append("file",file);const res=await fetch(`${BASE}/meetings/${id}/transcript/upload`,{method:"POST",body:form});if(!res.ok){const error=await res.json().catch(()=>null);throw new Error(error?.error?.message??"Transcript upload failed");}return res.json() as Promise<{segments_created:number}>}
};
