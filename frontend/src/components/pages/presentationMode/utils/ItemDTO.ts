export type ItemDTO = {
    name: string;
    id?: string;
    subNodes?: ItemDTO[];
  }