import os

class KotlinGenerator:
    def __init__(self, plugin_name, main_url):
        self.plugin_name = plugin_name
        self.main_url = main_url

    def generate_provider_code(self, catalog_items):
        items_code = ""
        for item in catalog_items:
            title = item['title'].replace('"', '\\"')
            url = item['url']
            poster = item['poster']
            items_code += f'''
        items.add(
            newHomePageList(
                name = "{title}",
                url = "{url}",
                type = TvType.Movie,
                posterUrl = "{poster}"
            )
        )'''

        code = f'''package com.cloudstream

import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.*

class {self.plugin_name}Provider : MainAPI() {{
    override var mainUrl = "{self.main_url}"
    override var name = "{self.plugin_name}"
    override val hasMainPage = true
    override var lang = "en"
    override val supportedTypes = setOf(TvType.Movie, TvType.TvSeries)

    override async fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse {{
        val items = mutableListOf<HomePageList>()
        {items_code}
        return newHomePageResponse(
            list = HomePageList(
                name = "Latest Releases",
                list = items
            ),
            hasNext = false
        )
    }}
}}
'''
        return code

    def save_code(self, code, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"[GENERATOR] Fail Kotlin berjaya disimpan di: {output_path}")
