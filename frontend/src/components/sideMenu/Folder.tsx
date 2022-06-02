import {FolderDetails} from "./FolderDetails";

export type Folder = {
    id: number;
    uid: string;
    title: string;
    folderDetails: FolderDetails[];
}