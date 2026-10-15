// Sets the page title and description, and repeats them in the Open Graph and Twitter tags
// so links shared in messengers and social apps show the right preview.
export function usePageMeta(title: () => string, description: () => string) {
  const full = () => `${title()} | Doz`
  useSeoMeta({
    title,
    description,
    ogTitle: full,
    ogDescription: description,
    twitterTitle: full,
    twitterDescription: description,
  })
}
