import { UnwrappedItemDTO } from "./UnwrappedItemDTO"

export const unwrapStructure = (data: any): UnwrappedItemDTO[] => {
    for (const el of data){
      if (el.subNodes) return unwrapStructure(el.subNodes)
    }
    
    return data
  }