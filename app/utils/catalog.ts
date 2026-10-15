import type { CatalogEntry } from '../../lib/types'
import catalogJson from '../generated/catalog.json'

export const catalog = catalogJson as CatalogEntry[]
