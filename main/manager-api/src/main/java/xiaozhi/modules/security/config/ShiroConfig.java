package xiaozhi.modules.security.config;

import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

import org.apache.shiro.mgt.SecurityManager;
import org.apache.shiro.session.mgt.SessionManager;
import org.apache.shiro.spring.LifecycleBeanPostProcessor;
import org.apache.shiro.spring.security.interceptor.AuthorizationAttributeSourceAdvisor;
import org.apache.shiro.spring.web.ShiroFilterFactoryBean;
import org.apache.shiro.web.config.ShiroFilterConfiguration;
import org.apache.shiro.web.mgt.DefaultWebSecurityManager;
import org.apache.shiro.web.session.mgt.DefaultWebSessionManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import jakarta.servlet.Filter;
import xiaozhi.modules.security.oauth2.Oauth2Filter;
import xiaozhi.modules.security.oauth2.Oauth2Realm;
import xiaozhi.modules.security.secret.ServerSecretFilter;
import xiaozhi.modules.sys.service.SysParamsService;

/**
 * Shiro 的配置文件
 * Copyright (c) 人人开源 All rights reserved.
 * Website: https://www.renren.io
 */
@Configuration
public class ShiroConfig {

    @Bean
    public DefaultWebSessionManager sessionManager() {
        DefaultWebSessionManager sessionManager = new DefaultWebSessionManager();
        sessionManager.setSessionValidationSchedulerEnabled(false);
        sessionManager.setSessionIdUrlRewritingEnabled(false);

        return sessionManager;
    }

    @Bean("securityManager")
    public SecurityManager securityManager(Oauth2Realm oAuth2Realm, SessionManager sessionManager) {
        DefaultWebSecurityManager securityManager = new DefaultWebSecurityManager();
        securityManager.setRealm(oAuth2Realm);
        securityManager.setSessionManager(sessionManager);
        securityManager.setRememberMeManager(null);
        return securityManager;
    }

    @Bean("shiroFilter")
    public ShiroFilterFactoryBean shirFilter(SecurityManager securityManager, SysParamsService sysParamsService) {
        ShiroFilterConfiguration config = new ShiroFilterConfiguration();
        config.setFilterOncePerRequest(true);

        ShiroFilterFactoryBean shiroFilter = new ShiroFilterFactoryBean();
        shiroFilter.setSecurityManager(securityManager);
        shiroFilter.setShiroFilterConfiguration(config);

        Map<String, Filter> filters = new HashMap<>();
        // oauth 过滤
        filters.put("oauth2", new Oauth2Filter());
        // 服务密钥过滤
        filters.put("server", new ServerSecretFilter(sysParamsService));
        shiroFilter.setFilters(filters);

        // 添加 Shiro 的内置过滤器
        /*
         * anon：无需认证就可以访问
         * authc：必须认证了才能让问
         * user：必须拥有，记住我功能，才能访问
         * perms：拥有对某个资源的权限才能访问
         * role：拥有某个角色权限才能访问
         */
        Map<String, String> filterMap = new LinkedHashMap<>();
        // OTA 接口（ESP32 设备和智控台使用）
        filterMap.put("/ota/**", "anon");
        filterMap.put("/otaMag/download/**", "anon");
        // 智控台接口（带/xiaozhi 前缀，nginx 转发后使用）
        filterMap.put("/xiaozhi/ota/**", "anon");
        filterMap.put("/xiaozhi/otaMag/download/**", "anon");
        filterMap.put("/xiaozhi/webjars/**", "anon");
        filterMap.put("/xiaozhi/druid/**", "anon");
        filterMap.put("/xiaozhi/v3/api-docs/**", "anon");
        filterMap.put("/xiaozhi/doc.html", "anon");
        filterMap.put("/xiaozhi/favicon.ico", "anon");
        filterMap.put("/xiaozhi/user/captcha", "anon");
        filterMap.put("/xiaozhi/user/smsVerification", "anon");
        filterMap.put("/xiaozhi/user/login", "anon");
        filterMap.put("/xiaozhi/user/pub-config", "anon");
        filterMap.put("/xiaozhi/user/register", "anon");
        filterMap.put("/xiaozhi/user/retrieve-password", "anon");
        // 不带/xiaozhi 前缀的路径（nginx 转发后的实际路径）
        filterMap.put("/webjars/**", "anon");
        filterMap.put("/druid/**", "anon");
        filterMap.put("/v3/api-docs/**", "anon");
        filterMap.put("/doc.html", "anon");
        filterMap.put("/favicon.ico", "anon");
        filterMap.put("/user/captcha", "anon");
        filterMap.put("/user/smsVerification", "anon");
        filterMap.put("/user/login", "anon");
        filterMap.put("/user/pub-config", "anon");
        filterMap.put("/user/register", "anon");
        filterMap.put("/user/retrieve-password", "anon");
        // 将 config 路径使用 server 服务过滤器
        filterMap.put("/config/**", "server");
        filterMap.put("/xiaozhi/config/**", "server");
        filterMap.put("/agent/chat-history/report", "server");
        filterMap.put("/xiaozhi/agent/chat-history/report", "server");
        filterMap.put("/agent/chat-history/download/**", "anon");
        filterMap.put("/xiaozhi/agent/chat-history/download/**", "anon");
        filterMap.put("/agent/chat-summary/**", "server");
        filterMap.put("/xiaozhi/agent/chat-summary/**", "server");
        filterMap.put("/agent/play/**", "anon");
        filterMap.put("/xiaozhi/agent/play/**", "anon");
        filterMap.put("/voiceClone/play/**", "anon");
        filterMap.put("/xiaozhi/voiceClone/play/**", "anon");
        filterMap.put("/**", "oauth2");
        shiroFilter.setFilterChainDefinitionMap(filterMap);

        return shiroFilter;
    }

    @Bean("lifecycleBeanPostProcessor")
    public LifecycleBeanPostProcessor lifecycleBeanPostProcessor() {
        return new LifecycleBeanPostProcessor();
    }

    @Bean
    public AuthorizationAttributeSourceAdvisor authorizationAttributeSourceAdvisor(SecurityManager securityManager) {
        AuthorizationAttributeSourceAdvisor advisor = new AuthorizationAttributeSourceAdvisor();
        advisor.setSecurityManager(securityManager);
        return advisor;
    }
}
