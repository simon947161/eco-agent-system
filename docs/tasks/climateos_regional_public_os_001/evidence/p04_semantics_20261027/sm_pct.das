Attributes {
    time {
        String name "time";
        String standard_name "time";
        String long_name "time";
        String units "days since 1900-01-01";
        String calendar "gregorian";
        String bounds "time_bounds";
        UInt32 _ChunkSizes 1024;
    }
    latitude {
        String name "latitude";
        String standard_name "latitude";
        String long_name "latitude";
        String units "degrees_north";
        UInt32 _ChunkSizes 681;
    }
    longitude {
        String name "longitude";
        String standard_name "longitude";
        String long_name "longitude";
        String units "degrees_east";
        UInt32 _ChunkSizes 841;
    }
    time_bounds {
        UInt32 _ChunkSizes 1, 2;
    }
    sm_pct {
        Float32 _FillValue -999.0;
        String name "sm_pct";
        String standard_name "sm_pct";
        String long_name "Total rootzone soil moisture (0-100 cm)";
        String units "fraction of fullness";
        UInt32 _ChunkSizes 1, 128, 128;
    }
    NC_GLOBAL {
        String var_name "sm_pct";
        String title "Australian Landscape Water Balance AWRA-L Model";
        String Description "This data is provided by the Bureau of Meteorology and can be further visualised at www.bom.gov.au/water/landscape . The data has been simulated using the Australian Water Resource Assessment Modelling System (AWRA MS).";
        String summary "Data produced by Bureau of Meteorology Australian Water Resources Assessment Landscape Model (AWRA-L)";
        String source "AWRA-L";
        String date_created "2021-09-20T00:48:31";
        String Conventions "CF-1.6, ACDD-1.3";
        String institution "Bureau of Meteorology";
        String email "awrams@bom.gov.au";
        String url "http://www.bom.gov.au/water/landscape";
        String date_modified "2021-09-20T00:48:31";
    }
    DODS_EXTRA {
        String Unlimited_Dimension "time";
    }
}
