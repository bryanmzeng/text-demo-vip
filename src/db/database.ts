import Dexie, { Table } from 'dexie';

export interface TextEntry {
  id?: number;
  content: string;
  timestamp: Date;
}

export class TextDatabase extends Dexie {
  textEntries!: Table<TextEntry>;

  constructor() {
    super('textDatabase');
    this.version(1).stores({
      textEntries: '++id, timestamp'
    });
  }
}

export const db = new TextDatabase();