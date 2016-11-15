/******************************************************************************************************

 Copyright (c) 2016 EPAM Systems Inc.

 Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 *****************************************************************************************************/

package com.epam.dlab.auth.ldap;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;

import org.apache.directory.ldap.client.api.LdapConnectionConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.epam.dlab.auth.ldap.core.Request;
import com.epam.dlab.client.mongo.MongoServiceFactory;
import com.fasterxml.jackson.annotation.JsonProperty;

import io.dropwizard.Configuration;

public class SecurityServiceConfiguration extends Configuration {

	private static final String MONGO = "mongo";

	protected final Logger LOG = LoggerFactory.getLogger(this.getClass());
	
	public SecurityServiceConfiguration() {
		super();
	}
	
	private boolean userInfoPersistenceEnabled = false;
	
	@JsonProperty
	private long inactiveUserTimeoutMillSec;
	
	public long getInactiveUserTimeoutMillSec() {
		return inactiveUserTimeoutMillSec;
	}

	@JsonProperty
	public boolean isUserInfoPersistenceEnabled() {
		return userInfoPersistenceEnabled;
	}

	@JsonProperty
	private List<Request> ldapSearch;
	
	public List<Request> getLdapSearch() {
		return ldapSearch;
	}

	@JsonProperty
	private String ldapBindTemplate;
	
	@JsonProperty
	private Map<String,String> ldapConnectionConfig = new HashMap<String, String>();
	private LdapConnectionConfig _ldapConnectionConfig;
	
	public LdapConnectionConfig getLdapConnectionConfig() {
		if(_ldapConnectionConfig == null) {
			_ldapConnectionConfig = new LdapConnectionConfig();
			_ldapConnectionConfig.setLdapHost(ldapConnectionConfig.get("ldapHost"));
			_ldapConnectionConfig.setLdapPort(Integer.parseInt(ldapConnectionConfig.get("ldapPort")));
			_ldapConnectionConfig.setName(ldapConnectionConfig.get("name"));
			_ldapConnectionConfig.setCredentials(ldapConnectionConfig.get("credentials"));
			//TODO: add all configurable properties
			//      from the LdapConnectionConfig class
		}
		return _ldapConnectionConfig;
		
	}

	public String getLdapBindTemplate() {
		return ldapBindTemplate;
	}
	
  @Valid
  @NotNull
  @JsonProperty(MONGO)
  private MongoServiceFactory mongoFactory = new MongoServiceFactory();

    public MongoServiceFactory getMongoFactory() {
        return mongoFactory;
    }
}