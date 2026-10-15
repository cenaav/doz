import Ajv2020 from 'ajv/dist/2020'
import addFormats from 'ajv-formats'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'
import type { DataSet, Drug } from '../types'
import { collectRefs } from './refs'

/** Validates a data set. `schemaRoot` is the directory that contains `schema/`. Returns [] when valid. */
export function validateDataSet(ds: DataSet, schemaRoot: string): string[] {
  const errors: string[] = []
  const ajv = new Ajv2020({ allErrors: true })
  addFormats(ajv)
  for (const n of ['drug', 'source', 'disease', 'category', 'collection'])
    ajv.addSchema(JSON.parse(readFileSync(join(schemaRoot, 'schema', `${n}.schema.json`), 'utf8')))
  const schema = (n: string) => ajv.getSchema(`${n}.schema.json`)!
  const check = (name: string, fn: ReturnType<typeof schema>, value: unknown) => {
    if (!fn(value)) for (const e of fn.errors ?? []) errors.push(`${name}: ${e.instancePath || '/'} ${e.message}`)
  }
  check('sources.json', schema('source'), ds.sources)
  check('diseases.json', schema('disease'), ds.diseases)
  check('categories.json', schema('category'), ds.categories)
  check('collections.json', schema('collection'), ds.collections ?? [])
  const drugSchema = schema('drug')
  for (const { path, drug } of ds.drugs) check(path, drugSchema, drug)
  if (errors.length) return errors

  for (const s of ds.sources) if (!s.url && s.license !== 'pending') errors.push(`sources.json: ${s.id} has no online url`)
  const sourceIds = new Set(ds.sources.map((s) => s.id))
  const diseaseIds = new Set(ds.diseases.map((d) => d.id))
  const categoryIds = new Set(ds.categories.map((c) => c.id))
  const dup = (ids: string[], what: string) => {
    const seen = new Set<string>()
    for (const id of ids) {
      if (seen.has(id)) errors.push(`duplicate ${what} id: ${id}`)
      seen.add(id)
    }
  }
  dup(ds.sources.map((s) => s.id), 'source')
  dup(ds.diseases.map((d) => d.id), 'disease')
  dup(ds.categories.map((c) => c.id), 'category')
  dup(ds.drugs.map((d) => d.drug.id), 'drug')

  for (const r of collectRefs(ds.diseases)) if (!sourceIds.has(r.source)) errors.push(`diseases.json: unknown source ${r.source}`)
  const drugIds = new Set(ds.drugs.map((d) => d.drug.id))
  for (const c of ds.collections ?? []) for (const id of c.drugs) if (!drugIds.has(id)) errors.push(`collections.json: ${c.id} unknown drug ${id}`)
  const catAtc = new Map(ds.categories.map((c) => [c.id, c.atc]))
  for (const { path, drug } of ds.drugs) {
    const main = drug.atc?.[0]?.[0]
    if (main && catAtc.get(drug.category) !== main) errors.push(`${path}: ATC ${drug.atc![0]} belongs in the category for group ${main}`)
  }
  for (const { path, drug } of ds.drugs) errors.push(...checkDrug(path, drug, sourceIds, diseaseIds, categoryIds))
  return errors
}

function checkDrug(path: string, d: Drug, sourceIds: Set<string>, diseaseIds: Set<string>, categoryIds: Set<string>): string[] {
  const e: string[] = []
  const expectedPath = `drugs/${d.category}/${d.id}.json`
  if (path.replaceAll('\\', '/') !== expectedPath) e.push(`${path}: must be at ${expectedPath}`)
  if (!categoryIds.has(d.category)) e.push(`${path}: unknown category ${d.category}`)
  for (const r of collectRefs(d)) if (!sourceIds.has(r.source)) e.push(`${path}: unknown source ${r.source}`)

  const formIds = new Set(d.formulations.map((f) => f.id))
  const regIds = new Set(d.regimens.map((r) => r.id))
  for (const r of d.regimens) {
    if (!diseaseIds.has(r.disease)) e.push(`${path}: regimen ${r.id} unknown disease ${r.disease}`)
    for (const f of r.allowedFormulations ?? []) if (!formIds.has(f)) e.push(`${path}: regimen ${r.id} unknown formulation ${f}`)
    const unit = r.unit ?? 'mg'
    if (r.type !== 'notCalculated' && unit !== 'mL') {
      for (const f of d.formulations.filter((f) => !r.allowedFormulations || r.allowedFormulations.includes(f.id)))
        if (f.concentration.unit !== unit) e.push(`${path}: regimen ${r.id} unit ${unit} ≠ formulation ${f.id} unit ${f.concentration.unit}`)
    }
    if (r.doseComponent) {
      for (const f of d.formulations) if (f.components && !f.components[r.doseComponent]) e.push(`${path}: formulation ${f.id} lacks component ${r.doseComponent}`)
    }
    if (r.type !== 'notCalculated' && !d.examples.some((x) => x.regimen === r.id)) e.push(`${path}: regimen ${r.id} has no example`)
  }
  for (const x of d.examples) {
    if (!regIds.has(x.regimen)) e.push(`${path}: example unknown regimen ${x.regimen}`)
    if (!formIds.has(x.formulation)) e.push(`${path}: example unknown formulation ${x.formulation}`)
    if (x.input.ageDays == null && x.input.ageMonths == null && x.input.ageYears == null) e.push(`${path}: example needs an age`)
  }
  if (d.review.status === 'verified' && (!d.review.reviewer || !d.review.date)) e.push(`${path}: verified needs reviewer and date`)
  return e
}
