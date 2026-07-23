package com.cloudstream

import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.*

class UncenxProvider : MainAPI() {
    override var mainUrl = "https://uncenx.com"
    override var name = "Uncenx"
    override val hasMainPage = true
    override var lang = "en"
    override val supportedTypes = setOf(TvType.Movie, TvType.TvSeries)

    override async fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse {
        val items = mutableListOf<HomePageList>()
        
        items.add(
            newHomePageList(
                name = "แอบถ่ายเดทส่วนตัวจริงๆ ของมาริ รินัทสึ",
                url = "https://uncenx.com/tppn-155-uncen",
                type = TvType.Movie,
                posterUrl = "https://i.uncenxcdn.com/V3HD3Q_w-MWc/thumb.jpg"
            )
        )
        items.add(
            newHomePageList(
                name = "ภรรยาแอบคบชู้ที่เรียวกัง 07 - มิอุมิ คาตาฮิระ",
                url = "https://uncenx.com/aby-007-uncen",
                type = TvType.Movie,
                posterUrl = "https://i.uncenxcdn.com/zJw_3USlU-wr/thumb.jpg"
            )
        )
        items.add(
            newHomePageList(
                name = "Kasumi Haruka เปิดตัวหนังอาร์ตผู้ใหญ่ครั้งแรก",
                url = "https://uncenx.com/avop-126-uncen",
                type = TvType.Movie,
                posterUrl = "https://i.uncenxcdn.com/s_YnI4-GHyxi/thumb.jpg"
            )
        )
        items.add(
            newHomePageList(
                name = "อยู่ด้วยกัน 5 วันกับสาวเพื่อนสมัยเด็กจอมปากร้าย นานะ ยากิ",
                url = "https://uncenx.com/midv-230-uncen",
                type = TvType.Movie,
                posterUrl = "https://i.uncenxcdn.com/Goqg_wveG-Ml/thumb.jpg"
            )
        )
        return newHomePageResponse(
            list = HomePageList(
                name = "Latest Releases",
                list = items
            ),
            hasNext = false
        )
    }
}
