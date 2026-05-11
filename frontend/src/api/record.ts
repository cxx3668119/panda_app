import { get, post } from "@/api/client";
import type { UserRecord } from "@/types";

export async function getRecordList() {
  return get<UserRecord[]>("/records/list");
}

export async function addRecord(record: UserRecord) {
  return post<{ success: true }>("/records/create", record);
}

export async function updateRecord(record: UserRecord) {
  return post<UserRecord>("/records/update", {
    id: record.id,
    name: record.name,
    birthday: record.birthday,
    gender: record.gender,
    birthplace: record.birthplace,
  });
}

export async function deleteRecord(recordId: number | string) {
  return post<{ success: true }>("/records/delete", { id: recordId });
}
