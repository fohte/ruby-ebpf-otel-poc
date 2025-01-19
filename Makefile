PUBLIC_IP = $(shell op plugin run -- aws ec2 describe-instances --filters "Name=tag:Name,Values=ebpf-sandbox" | jq -r '.Reservations[].Instances[].PublicIpAddress')
SSH_USERNAME := ec2-user
SSH = ssh $(SSH_USERNAME)@$(PUBLIC_IP)

# === remote ===
.PHONY: ssh
ssh:
	$(SSH)

.PHONY: deploy
deploy:
	rg --files | rsync -av --files-from=- . $(SSH_USERNAME)@$(PUBLIC_IP):~/poc/
	$(SSH) 'sudo ln -sf $$HOME/poc/etc/otelcol/config.yaml /etc/otelcol/config.yaml'
# === remote ===

# === local ===
.PHONY: run-http
run-http:
	bundle exec ruby src/test.rb

.PHONY: run-bpf
run-bpf:
	sudo -E python src/poc.py
# === local ===
