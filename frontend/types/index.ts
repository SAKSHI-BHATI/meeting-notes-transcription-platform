export type Meeting = { id:number; title:string; occurred_at:string; duration_ms:number; source:string; participant_names:string[]; action_item_count:number; created_at?:string; updated_at?:string };
export type Segment = {id:number; speaker_name:string; start_time_ms:number; end_time_ms:number; content:string};
export type Summary = {meeting_id:number; overview:string; key_points:string[]; decisions:string[]; provider:string};
export type Topic = {id:number;label:string;start_time_ms:number|null};
export type ActionItem = {id:number;meeting_id:number;title:string;description:string|null;assignee_id:number|null;assignee_name:string|null;due_date:string|null;priority:"low"|"medium"|"high";status:"open"|"completed";created_at:string;updated_at:string};
export type GlobalSearchResult = {type:"meeting"|"transcript";meeting_id:number;meeting_title:string;occurred_at:string;participant_names:string[];snippet:string;speaker_name?:string;start_time_ms:number|null};
