from oauth import authorize_creds

creds = 'client_secret.json'

webmasters_service = authorize_creds(creds)

site_list = webmasters_service.sites().list().execute()


# Filtrar sitios verificados que sean páginas (http...) o dominios (sc-domain...)
verified_sites = [site for site in site_list.get('siteEntry', [])
    if site.get('permissionLevel') != 'siteUnverifiedUser' and (
        site['siteUrl'].startswith('http') or site['siteUrl'].startswith('sc-domain:')
    )
]

print(verified_sites)