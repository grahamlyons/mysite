title: Hello World with Tomcat and Maven
date: 2013-06-02
url_code: hello-world-with-tomcat-and-maven

Generating a webapp structure:

    mvn archetype:generate -DgroupId=org.example -DartifactId=hello -DarchetypeArtifactId=maven-archetype-webapp -DinteractiveMode=false

See this structure (cd into 'hello' directory):

    [user@host hello]# tree
    .
    |-- pom.xml
    `-- src
        `-- main
            |-- resources
            `-- webapp
                |-- WEB-INF
                |   `-- web.xml
                `-- index.jsp

    5 directories, 3 files

### Add a Servlet

Create directory structure for Java classes and create the servlet file:

    mkdir -p src/main/java/org/example/
    touch src/main/java/org/example/HelloServlet.java

Remove the index.jsp file because we're going to use a Servlet instead:

    [user@host hello]# rm -f src/main/webapp/index.jsp

Add the following content to HelloServlet.java:

    // Reflecting the directory structure where the file lives
    package org.example;

    import javax.servlet.http.HttpServlet;
    import javax.servlet.ServletException;
    import javax.servlet.http.HttpServletRequest;
    import javax.servlet.http.HttpServletResponse;

    import java.io.IOException;
    import java.io.PrintWriter;

    public class HelloServlet extends HttpServlet {

        protected void doGet(HttpServletRequest request,
                             HttpServletResponse response) throws ServletException, IOException
        {
            // Very simple - just return some plain text
            PrintWriter writer = response.getWriter();
            writer.print("Hello World");
        }
    }

Add the following content to the web.xml file:

    <?xml version="1.0" encoding="UTF-8"?>
    <web-app version="2.4" xmlns="http://java.sun.com/xml/ns/j2ee"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">

        <display-name>Hello World Web Application</display-name>

        <servlet>
            <servlet-name>HelloServlet</servlet-name>
            <servlet-class>org.example.HelloServlet</servlet-class>
        </servlet>

        <servlet-mapping>
            <servlet-name>HelloServlet</servlet-name>
            <url-pattern>/</url-pattern>
        </servlet-mapping>

    </web-app>

The XML config above maps a URL to the Servlet class.

### Building and Deploying

We need to get a Tomcat instance to run the Servlet in:

    sudo apt-get install tomcat7 -y

The servlet api JAR is included in the Tomcat installation so it doesn't need to be bundled in the war file, however it is required for compiling the classes. The following dependency needs to be added to the pom.xml:

    <dependencies>
        ...
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>servlet-api</artifactId>
            <version>2.5</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

The 'scope' tells Maven that it is already provided so doesn't need to be included.

In the 'hello' directory in the workspace run the following commands:

    mvn clean package \
    rm -rf /usr/local/apache-tomcat-forge-services/webapps/my-webapp \
    /bin/cp -f target/my-webapp.war /usr/local/apache-tomcat-forge-services/webapps/ \
    service apache-tomcat-forge-services restart

Then follow the log file to check for problems:

    tail -f /data/app-logs/apache-tomcat-forge-services/catalina.out

If the war file is placed into the 'webapps' directory of the Tomcat installation then it's picked up and unpacked when the server is starting up. The 'rm -rf...' step is necessary to remove an existing installation but for the first time, that won't be there.

### Hitting the endpoint

Once the server has started without any errors the application can be accessed by hitting the local IP address on the appropriate port and including the webapp (the name of the war file) in the URL:

    [user@host ~]# http_proxy= curl -D - http://127.0.0.1:8134/hello/
    HTTP/1.1 200 OK
    Content-Length: 11
    Date: Tue, 05 Mar 2013 13:32:42 GMT
    Server: Apache

    Hello World

The port that Tomcat listens on is configured in the 'conf/server.xml' under the installation directory (/usr/local/apache-tomcat-forge-services in this case). The information about the IP and port are also available in the log:

    INFO: Starting Coyote HTTP/1.1 on http-0.0.0.0-8134

Listening on port 8134 and all IP addresses here.

### Limitations

This servlet doesn't know about the URL at all so we can hit anything under '/' and it'll respond in exactly the same way:

    [user@host ~]# http_proxy= curl -D - http://127.0.0.1:8134/my-webapp/what/the/hell/is/this?
    HTTP/1.1 200 OK
    Content-Length: 11
    Date: Tue, 05 Mar 2013 13:46:41 GMT
    Server: Apache

    Hello World

