# set -ex
function call_the_route {
    body=$1
    echo 'curl https://'${application_domain}'/murano \
        -H "content-type: application/json" \
        -d '${body}' -i'
    curl https://${application_domain}/murano \
        -H "content-type: application/json" \
        -d "${body}" -i

}

# application_domain="teststacy.apps.exosite-staging.io"
application_domain="teststacy.apps.exosite.io"

bodys=('{"service":"Keystore","parameters":{}}'
'{"operation":"set","parameters":{}}'
'{"service":[],"operation":"set","parameters":{}}'
'{"service":{},"operation":"set","parameters":{}}'
'{"service":{},"operation":"set"}'
'{"service":"keystore","operation":"kv","parameters":{}}'
'{"service":"keystore","operation":"","parameters":{}}'
'{"service":"kv","operation":"set","parameters":{}}'
'{"service":"","operation":"set","parameters":{}}'
'{"service":1234,"operation":"set","parameters":{}}')


for i in "${bodys[@]}"; do
# {panel:title=Scenario: post request and body without operation}
    echo "* POST with body $i {code}"
    call_the_route ${i}
    echo "{code}"
done