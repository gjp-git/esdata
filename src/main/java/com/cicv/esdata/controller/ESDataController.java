package com.cicv.esdata.controller;

import com.cicv.esdata.util.StringUtils;
import org.apache.http.HttpHost;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.search.sort.SortOrder;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@RestController
@CrossOrigin
@RequestMapping(value = "/cicv/scene")
public class ESDataController {
    @Value("${com.cicv.fdfs.service.ip}")
    private String hostname;

    @Value("${com.cicv.fdfs.service.post}")
    private int post;

    private int dataNum = 300;

    @RequestMapping(value = "/")
    public String HelloWorld() {
        return "welcome";
    }

    @PostMapping("/getScenceByCity")
    public String search(@RequestBody Map<String, String> args) {
        //TODO： 改为连接池
        RestHighLevelClient client = new RestHighLevelClient(
                RestClient.builder(
                        new HttpHost(hostname, post, "http")));
        String city = null;
        String timestamp = null;
        if (args.containsKey("city")) {
            city = args.get("city");
        } else {
            return "No param named \"city\"!";
        }
        if (args.containsKey("timestamp")) {
            timestamp = args.get("timestamp");
            if (timestamp.length() != 10 || !StringUtils.isNumeric(timestamp)) {
                return "Incorrect value of \"timestamp\" !";
            }
            timestamp = timestamp + "0";//10hz
        }

        SearchRequest searchRequest = new SearchRequest("scene_data"); //指定posts索引
        searchRequest.types("scene");

        SearchSourceBuilder sourceBuilder = new SearchSourceBuilder(); //构造一个默认配置的对象
        sourceBuilder.query(QueryBuilders.termQuery("city", city)); //设置查询始
        if (timestamp != null)
            sourceBuilder.postFilter(QueryBuilders.rangeQuery("timestamp").from(new Long(timestamp)));
        sourceBuilder.sort("timestamp", SortOrder.ASC);
        sourceBuilder.size(dataNum);
        sourceBuilder.timeout(new TimeValue(60, TimeUnit.SECONDS)); //设置超时时间

        searchRequest.source(sourceBuilder);

        SearchResponse searchResponse = null;
        String result = null;
        try {
            searchResponse = client.search(searchRequest, RequestOptions.DEFAULT);
            SearchHit[] searchHit = searchResponse.getHits().getHits();
            if (searchHit.length > 0) {
                JSONArray rs = new JSONArray();
                JSONObject preHit = new JSONObject(searchHit[0].getSourceAsString());
                long startTime = Long.parseLong(preHit.getString("timestamp"));
                long searchTime = Long.parseLong(timestamp);
                if (startTime - searchTime > dataNum * 0.1) {
                    result = "[]";
                } else {
                    for (SearchHit hit : searchHit) {
                        JSONObject curHit = new JSONObject(hit.getSourceAsString());
                        long time = Long.parseLong(curHit.getString("timestamp"));
                        long preTime = Long.parseLong(preHit.getString("timestamp"));
                        if (time - preTime > 5)
                            break;
                        rs.put(curHit);
                        preHit = curHit;
                    }
                    result = rs.toString();
                }
            } else {
                result = "[]";
            }

            client.close();
        } catch (IOException | NumberFormatException | NullPointerException e) {
            e.printStackTrace();
            result = "{\"state\":\"failure\",\"info\":\"Something went wrong.\"}";
        }
        return result;
    }
}
